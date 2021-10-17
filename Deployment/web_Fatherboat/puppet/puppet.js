const puppeteer = require("puppeteer");
const express = require('express');

app = express();
app.use(express.json())
const PORT = 9000;

async function puppet(url) {
  const browser = await puppeteer.launch({args: ['--no-sandbox', '--disable-setuid-sandbox']});
  const page = await browser.newPage();
  cookies = [{
    'name': "token",
    'value': "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhZG1pbiI6ImZhbHNlIn0.nblNyVlpVcbsLvafywO2zwiv5GiIuaArrJzQhfWipu4",
    'url': url}]
  await page.setCookie(...cookies);
  await page.goto(url)
  setTimeout(async () => {
    await browser.close();
  }, 1000);
}

app.post('/', function (req, res) {
  puppet(req.body.url)
  res.send('success')
})

app.listen(PORT)
