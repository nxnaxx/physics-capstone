const express = require('express');
const app = express();
const fs = require('fs');
const { format } = require('path');
const port = 8000;

app.use(express.json()); // for parsing application/json
app.use(express.urlencoded({ extended: true })); // for parsing application/x-www-form-urlencoded

let list = [
  { barcode: '1234', product: '빠삐코', price: '1000' },
  { barcode: '1235', product: '더위사냥', price: '2000' },
  { barcode: '1236', product: '설레임', price: '3000' },
  { barcode: '1237', product: '월드콘', price: '4000' },
  { barcode: '1238', product: '베스킨라빈스 쿼터', price: '5000' },
];

let data = [];
app.get('/', (req, res) => {
  let invoice = '';
  for (let i = 0; i < data.length; i++) {
    for (let d of list) {
      if (parseInt(d.barcode) == parseInt(data[i])) {
        invoice += `
          상품명 : ${d.product}<br>
          가격 : ${d.price} 원<br>
          바코드 : ${d.barcode}<br><br>
        `;
        break;
      }
    }
  }
  res.send(invoice);
});

app.post('/', (req, res) => {
  let { barcode } = req.body;

  for (let d of list) {
    if (parseInt(d.barcode) == parseInt(barcode)) {
      console.log(`
      상품명: ${d.product}<br>
      가격: ${d.price}원<br>
      바코드 : ${d.barcode}<br><br>
      `);
    }
  }
  data.push(barcode);
  res.end();
});

app.listen(port, () => {
  console.log(`Example app listening on port ${port}`);
});
