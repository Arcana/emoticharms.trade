'use strict';

var path = require('path');
var bourbon = require('node-bourbon').includePaths;

module.exports = {
    cache: true,
    entry: "./entry.js",
    output: {
        publicPath: "http://localhost:8080/"
    },
    module: {
        loaders: [
            { test: /bootstrap\/js\//, loader: 'imports?jQuery=jquery' },
            { test: /\.s(a|c)ss$/, loader: "style!css!sass?indentedSyntax&includePaths[]=" + bourbon },
            { test: /\.woff2?$/, loader: "url?limit=10000&mimetype=application/font-woff" },
            { test: /\.ttf$/, loader: "file" },
            { test: /\.eot$/, loader: "file" },
            { test: /\.svg$/, loader: "file" },
            { test: /\.png$/, loader: "file" }
        ]
    }
};
