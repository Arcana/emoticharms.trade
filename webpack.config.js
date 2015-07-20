'use strict';

var path = require('path');

module.exports = {
    cache: true,
    entry: "./entry.js",
    output: {
        path: path.join(__dirname, './app/build'),
        filename: "bundle.js"
    },
    module: {
        loaders: [
            { test: /bootstrap\/js\//, loader: 'imports?jQuery=jquery' },
            { test: /\.sass$/, loader: "style!css!sass" },
            { test: /\.woff2?$/, loader: "url?limit=10000&mimetype=application/font-woff" },
            { test: /\.ttf$/, loader: "file" },
            { test: /\.eot$/, loader: "file" },
            { test: /\.svg$/, loader: "file" }
        ]
    }
};
