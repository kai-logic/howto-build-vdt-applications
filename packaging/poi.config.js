/* eslint-disable */
const path = require('path');

module.exports = (options, req) => ({
  entry: './src/index.js',
  dist: './app/dist',
  html: {
    template: './index.html'
  },
  templateCompiler: false,
  extendWebpack(config) {
    // Extend webpack config with webpack-bundle-tracker for django-webpack-loader
    // to do its job when building for production
    const BundleTracker = require('webpack-bundle-tracker')
    config.plugin('bundle-tracker')
    .use(BundleTracker, [{filename: './app/webpack-stats.json'}]);

    // Change public path to match Django static path 
    config.output.publicPath('/static/')
  }
});

