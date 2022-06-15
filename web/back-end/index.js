const express = require('express');
const app = express();
const cors = require('cors');
const port = 3000;

const corsOptions = {
  origin: 'null',
  credentials: true,
};
app.use(cors(corsOptions));

const { WebSocketServer } = require('ws');
const wss = new WebSocketServer({ port: 3002 });

const mysql = require('mysql');
const connection = mysql.createConnection({
  host: 'localhost',
  user: 'root',
  password: 'mysql125',
  database: 'products_db',
});

connection.connect((err) => {
  if (err) console.log(err);
  else console.log('MYSQL_CONNECTED_SUCCESS');
});

app.get('/', (req, res) => {
  try {
    connection.query('SELECT * FROM products', (err, rows, fields) => {
      if (err) throw err;
      console.log(rows);
      return res.json({
        code: 'SUCCESS',
        data: rows,
      });
    });
  } catch (error) {
    console.log(error);
    return res.json({
      code: 'FAILED',
      msg: error.msg,
    });
  }
});

app.get('/items', (req, res) => {
  try {
    connection.query('SELECT * FROM items', (err, items) => {
      if (err) throw err;
      connection.query('SELECT * FROM products', (err, products) => {
        if (err) throw err;

        let result = [];
        let barcodes = [];

        items.forEach((item) => {
          let duplicate = false;
          for (let i = 0; i < barcodes.length; i++) {
            if (item.barcode == barcodes[i].barcode) {
              barcodes[i].cnt++;
              duplicate = true;
              break;
            }
          }
          if (!duplicate) {
            barcodes.push({ barcode: item.barcode, cnt: 1 });
          }
        });

        barcodes.forEach((i) => {
          products.forEach((p) => {
            if (p.barcode == i.barcode) {
              result.push({ data: p, count: i.cnt });
            }
          });
        });
        return res.json({
          code: 'SUCCESS',
          data: result,
        });
      });
    });
  } catch (error) {
    console.log(error);
    return res.json({
      code: 'FAILED',
      msg: error.msg,
    });
  }
});

// 바코드 찍었을때 값 입력용 API
app.post('/items', (req, res) => {
  try {
    const { barcode } = req.query;
    console.log('from py : ' + barcode);
    if (!barcode) throw 'BARCODE_NOT_FOUND';
    connection.query(`SELECT * FROM items WHERE barcode=${barcode}`, (err, items) => {
      console.log(items);
      if (items.length == 0) {
        connection.query(`INSERT INTO items (barcode) VALUES ("${barcode}")`, (err, result) => {
          if (err) {
            console.log(err);
            throw 'FAILED_TO_INSERT';
          }
          console.log('INSERTED_ITEM_SUCCESS');
          return res.json({
            code: 'SUCCESS',
            data: null,
          });
        });
      } else {
        return res.json({
          code: 'FAILED',
          data: null,
        });
      }
    });
  } catch (error) {
    console.log(error);
    return res.json({
      code: 'FAILED',
      data: null,
    });
  }
});

// 리스트에 있는 바코드 찍었을때 값 제거용 API
app.get('/items-delete', (req, res) => {
  try {
    const { barcode } = req.query;
    console.log(barcode);
    if (!barcode) throw 'BARCODE_NOT_FOUND';
    connection.query(`DELETE FROM items WHERE barcode  = "${barcode}"`, (err, result) => {
      if (err) {
        console.log(err);
        throw 'FAILED_TO_DELETE';
      }
      console.log('DELETED_ITEM_SUCCESS');
      return res.json({
        code: 'SUCCESS',
        data: null,
      });
    });
  } catch (error) {
    console.log(error);
    return res.json({
      code: 'FAILED',
      data: null,
    });
  }
});

wss.on('connection', (ws) => {
  // 데이터 수신 이벤트 바인드
  ws.on('message', (data) => {
    console.log(`Received from user: ${data}`);
    ws.send('submit');
  });
  ws.interval = setInterval(() => {
    if (ws.readyState == ws.OPEN) {
      connection.query('SELECT * FROM items', (err, items) => {
        if (err) throw err;
        connection.query('SELECT * FROM products', (err, products) => {
          if (err) throw err;

          let result = [];
          let barcodes = [];

          items.forEach((item) => {
            let duplicate = false;
            for (let i = 0; i < barcodes.length; i++) {
              if (item.barcode == barcodes[i].barcode) {
                barcodes[i].cnt++;
                duplicate = true;
                break;
              }
            }
            if (!duplicate) {
              barcodes.push({ barcode: item.barcode, cnt: 1 });
            }
          });

          barcodes.forEach((i) => {
            products.forEach((p) => {
              if (p.barcode == i.barcode) {
                result.push({ data: p, count: i.cnt });
              }
            });
          });
          ws.send(JSON.stringify(result, null, '\t'));
        });
      });
    }
  }, 1000);
});

app.listen(port, () => {
  console.log(`Server Running on port ${port}`);
});
