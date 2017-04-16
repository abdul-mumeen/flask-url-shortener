import express from 'express'
import webpack from 'webpack'
import path from 'path'
import config from '../webpack.config.dev'
import open from 'open'
import http from 'http'
import httpProxy from 'http-proxy'

/* eslint-disable no-console */
const proxy = httpProxy.createProxyServer({})
const port = 3000
const app = express()
const compiler = webpack(config)

app.use(require('webpack-dev-middleware')(compiler, {
  noInfo: true,
  publicPath: config.output.publicPath
}))

app.use(require('webpack-hot-middleware')(compiler))

app.all(/^\/api\/(.*)/, (req, res) => {
  proxy.web(req, res, { target: 'http://localhost:5000' })
})

app.get('*', function (req, res) {
  res.sendFile(path.join(__dirname, '../src/index.html'))
})

app.listen(port, function (err) {
  if (err) {
    console.log(err)
  } else {
    open(`http://localhost:${port}/main/`)
  }
})
