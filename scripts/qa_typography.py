import asyncio,json,urllib.parse,re
from bs4 import BeautifulSoup
from pathlib import Path
from playwright.async_api import async_playwright
ROOT=Path(__file__).resolve().parents[1]
HTML=BeautifulSoup((ROOT/'index.html').read_text(), 'html.parser')
for t in list(HTML.select('script,link[rel=stylesheet]')): t.decompose()
HTML.head.insert(0,HTML.new_tag('base',href='http://9mongkol.local/'))
for file in ['styles.css','storefront.css','celestial.css','insights.css','nine-mongkol.css','nine-motion.css','nine-readable.css']:
  css=(ROOT/'web'/file).read_text()
  css=re.sub(r'@import\s+url\([^;]*;', '', css)
  css=css.replace("url('assets/9mongkol/","url('web/assets/9mongkol/")
  t=HTML.new_tag('style')
  t.string=css
  HTML.head.append(t)
HTML=str(HTML)
async def main():
  async with async_playwright() as p:
    browser=await p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox','--disable-dev-shm-usage'])
    failures=[]
    for width,height in [(1440,950),(1024,768),(390,844),(320,740)]:
      page=await browser.new_page(viewport={'width':width,'height':height},device_scale_factor=1, reduced_motion='reduce')
      page_errors=[]
      page.on('pageerror',lambda e:page_errors.append(str(e)))
      async def asset_route(route):
        url=urllib.parse.urlparse(route.request.url)
        path=urllib.parse.unquote(url.path).lstrip('/')
        f=(ROOT/path).resolve()
        if f.is_file() and str(f).startswith(str(ROOT)):
          mime='image/svg+xml' if f.suffix=='.svg' else 'image/png' if f.suffix=='.png' else 'image/jpeg' if f.suffix in ('.jpg','.jpeg') else 'application/octet-stream'
          await route.fulfill(body=f.read_bytes(),content_type=mime)
        else: await route.abort()
      await page.route('**/*',asset_route)
      await page.set_content(HTML,wait_until='domcontentloaded')
      await page.evaluate('''() => { history.replaceState = ()=>{}; }''')
      for file in ['offline-data.js','offline-bridge.js','insights.js','app.js','nine-motion.js']:
        await page.add_script_tag(content=(ROOT/'web'/file).read_text())
      await page.wait_for_timeout(850)
      home=await page.evaluate('''() => {let q=s=>document.querySelector(s), fs=s=>q(s)?getComputedStyle(q(s)).fontSize:null;return {viewport:innerWidth,docWidth:document.documentElement.scrollWidth,hero:fs('.hero-main p'),service:fs('.service-text'),category:fs('.celestial-categories small'),nav:fs('.nav-item'),button:fs('.hero-inline-form button'),loaded:q('#metric-numbers')?.textContent,css:[...document.styleSheets].length,heroFilter:getComputedStyle(q('.hero-main p')).filter}}''')
      print('HOME',width,json.dumps(home,ensure_ascii=False), 'errors',page_errors)
      if width==390:
        tiny=await page.evaluate('''() => [...document.querySelectorAll('#view-overview *')].filter(e=>e.children.length===0 && e.textContent.trim().length>5 && e.getBoundingClientRect().width>0 && e.getBoundingClientRect().height>0 && parseFloat(getComputedStyle(e).fontSize)<14).slice(0,20).map(e=>({tag:e.tagName,cls:e.className,txt:e.textContent.slice(0,40),size:getComputedStyle(e).fontSize}))''')
        print('SMALL_TEXT_HOME',tiny)
        overflow=await page.evaluate('''() => {let a=document.querySelector('.sidebar'),r=a.getBoundingClientRect();return [...a.querySelectorAll('*')].filter(e=>e.getBoundingClientRect().right>r.right+3).slice(0,12).map(e=>({cls:e.className,html:e.textContent.slice(0,30),right:e.getBoundingClientRect().right,scroll:e.scrollWidth}))}''')
        print('SIDEBAR_OVER',overflow)
      if home['docWidth']>width+2:failures.append(f'horizontal overflow HOME {width}: {home["docWidth"]}')
      if width>=1061:
        nav=await page.evaluate('''() => {let s=document.querySelector('.sidebar'); return {client:s.clientWidth,scroll:s.scrollWidth}}''')
        print('NAV',width,nav)
        if nav['scroll']>nav['client']+3:failures.append(f'nav overflow {width}')
      else:
        await page.locator('#mobile-menu').click()
        assert 'open' in (await page.locator('#sidebar').get_attribute('class'))
        await page.evaluate("document.querySelector('#sidebar').classList.remove('open')")
      if width in (1440,390): await page.screenshot(path=str(ROOT/f'PREVIEW_v08_HOME_{width}.png'),full_page=False,animations='disabled')
      await page.locator('#hero-analyze-number').fill('0646429449')
      await page.locator('#hero-analyze-form button').click()
      await page.wait_for_timeout(950)
      report=await page.evaluate('''() => {let q=s=>document.querySelector(s),fs=s=>q(s)?getComputedStyle(q(s)).fontSize:null;return {active:q('.view.active')?.id,output:!q('#analysis-output')?.hidden,radar:!!q('.ni-radar'),reportP:fs('.ni-report-intro p'),adviceP:fs('.ni-advice-grid p'),traceP:fs('.ni-trace-row p'),docWidth:document.documentElement.scrollWidth}}''')
      print('REPORT',width,report,'errors',page_errors)
      if width==390:
        tiny=await page.evaluate('''() => [...document.querySelectorAll('#view-analyze *')].filter(e=>e.children.length===0 && e.textContent.trim().length>5 && e.getBoundingClientRect().width>0 && e.getBoundingClientRect().height>0 && parseFloat(getComputedStyle(e).fontSize)<14).slice(0,35).map(e=>({tag:e.tagName,cls:e.className,txt:e.textContent.slice(0,40),size:getComputedStyle(e).fontSize}))''')
        print('SMALL_TEXT_REPORT',tiny)
      if report['docWidth']>width+2:failures.append(f'horizontal overflow REPORT {width}: {report["docWidth"]}')
      if not report['output'] or not report['radar']: failures.append(f'report missing {width}')
      if width in (1440,390): await page.screenshot(path=str(ROOT/f'PREVIEW_v08_REPORT_{width}.png'),full_page=False,animations='disabled')
      await page.evaluate("document.querySelector('#view-analyze').classList.remove('active')")
      for v in ['explorer','careers','rules','sources']:
        await page.evaluate('(v)=>{document.querySelectorAll(".view").forEach(n=>n.classList.toggle("active",n.id==="view-"+v))}',v)
        if v=='explorer':
          await page.evaluate("document.querySelector('#view-explorer').classList.add('active')")
        await page.wait_for_timeout(70)
        w=await page.evaluate('document.documentElement.scrollWidth')
        if w>width+2:failures.append(f'horizontal overflow {v} {width}: {w}')
        if width==390 and v=='explorer': await page.screenshot(path=str(ROOT/'PREVIEW_v08_EXPLORER_390.png'),full_page=False,animations='disabled')

      if page_errors: failures+=page_errors
      await page.close()
    await browser.close()
    if failures: raise AssertionError('\n'.join(failures))
asyncio.run(main())
