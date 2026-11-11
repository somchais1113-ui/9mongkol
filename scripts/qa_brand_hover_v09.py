"""9มงคล v0.9 browser smoke test, using mocked local assets when local navigation is blocked."""
import asyncio,json,re,urllib.parse
from pathlib import Path
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright
ROOT=Path(__file__).resolve().parents[1]
S=BeautifulSoup((ROOT/'index.html').read_text(encoding='utf-8'),'html.parser')
for tag in list(S.select('script,link[rel=stylesheet]')):tag.decompose()
S.head.insert(0,S.new_tag('base',href='http://9mongkol.local/'))
for fname in ['styles.css','storefront.css','celestial.css','insights.css','nine-mongkol.css','nine-motion.css','nine-readable.css','nine-polish.css']:
 css=(ROOT/'web'/fname).read_text(encoding='utf-8')
 css=re.sub(r'@import\s+url\([^;]*;','',css)
 css=css.replace("url('assets/9mongkol/","url('web/assets/9mongkol/")
 tag=S.new_tag('style');tag.string=css;S.head.append(tag)
HTML=str(S)
async def main():
 async with async_playwright() as p:
  browser=await p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox','--disable-dev-shm-usage'])
  outcomes=[]
  for width,height in [(1440,960),(390,844)]:
   page=await browser.new_page(viewport={'width':width,'height':height},device_scale_factor=1)
   errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
   async def route_fn(route):
    url=urllib.parse.urlparse(route.request.url)
    path=urllib.parse.unquote(url.path).lstrip('/')
    f=(ROOT/path).resolve()
    if f.is_file() and str(f).startswith(str(ROOT)):
     mime='image/webp' if f.suffix=='.webp' else 'image/svg+xml' if f.suffix=='.svg' else 'image/png' if f.suffix=='.png' else 'image/jpeg' if f.suffix in ('.jpg','.jpeg') else 'application/octet-stream'
     await route.fulfill(body=f.read_bytes(),content_type=mime)
    else: await route.abort()
   await page.route('**/*',route_fn)
   await page.set_content(HTML,wait_until='domcontentloaded')
   await page.evaluate('history.replaceState=()=>{}')
   for fname in ['offline-data.js','offline-bridge.js','insights.js','app.js','nine-motion.js']:
    await page.add_script_tag(content=(ROOT/'web'/fname).read_text(encoding='utf-8'))
   await page.wait_for_timeout(1000)
   dat=await page.evaluate('''() => ({logoWidth:document.querySelector('.nine-nav-logo').naturalWidth,heroLogoWidth:document.querySelector('.nine-hero-badge').naturalWidth,shade:getComputedStyle(document.querySelector('.nine-brand-shade')).backgroundColor,documentWidth:document.documentElement.scrollWidth,viewport:innerWidth,counter:document.querySelector('#metric-numbers').textContent})''')
   card=page.locator('.service-card').first
   await card.scroll_into_view_if_needed()
   await page.wait_for_timeout(1100)
   before=await card.bounding_box()
   await card.hover();await page.wait_for_timeout(400)
   after=await card.bounding_box()
   dat['hover']={'deltaY':round(after['y']-before['y'],3),'deltaHeight':round(after['height']-before['height'],3),'transform':await card.evaluate('(e)=>getComputedStyle(e).transform')}
   await page.evaluate("window.scrollTo({top:0,behavior:'instant'})");await page.wait_for_timeout(250)
   await page.screenshot(path=str(ROOT/f'PREVIEW_v09_HOME_{width}.png'),full_page=False,animations='disabled')
   await page.locator('#hero-analyze-number').fill('0646429449')
   await page.locator('#hero-analyze-form button').click()
   await page.wait_for_timeout(1000)
   dat['reportVisible']=await page.locator('.ni-report').first.is_visible()
   await page.screenshot(path=str(ROOT/f'PREVIEW_v09_REPORT_{width}.png'),full_page=False,animations='disabled')
   dat['errors']=errors
   outcomes.append(dat)
   await page.close()
  await browser.close()
  (ROOT/'QA_v09_BROWSER_RESULTS.json').write_text(json.dumps(outcomes,ensure_ascii=False,indent=2),encoding='utf-8')
  print(json.dumps(outcomes,ensure_ascii=False,indent=2))
  assert all(x['documentWidth']<=x['viewport']+2 and x['logoWidth']>0 and x['heroLogoWidth']>0 and x['reportVisible'] and abs(x['hover']['deltaY'])<1 and not x['errors'] for x in outcomes)
asyncio.run(main())
