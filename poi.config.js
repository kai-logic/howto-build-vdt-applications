/*eslint-disable */
const path = require('path');
var fs = require('fs');


let devConfig = {};
try {
  devConfig = require('./poi.dev.config.js');
} catch (e) {
  console.info('> No dev config supplied');
}


module.exports = (options, req) => ({ 
  entry: './src/index.js',
  outDir: './app/dist',
  jsx: 'vue',
  fullBuild: false,
  // plugins: [
  //   require('@poi/plugin-eslint')({
  //     loaderOptions: {
  //       exclude: /node_modules/,
  //       configFile: '.eslintrc.js',
  //       fix: true
  //     },
  //     command: ['develop', 'build']
  //   })
  // ],
  chainWebpack(config, context) {
    // Extend webpack config with webpack-bundle-tracker for django-webpack-loader
    // to do its job when building for production

    if(context.command === 'build') {
      const BundleTracker = require('webpack-bundle-tracker')
      config.plugin('bundle-tracker')
        .use(BundleTracker, [{filename: './app/webpack-stats.json'}]);

      // Change public path to match Django static path 
      config.output.publicPath('/static/')
    }
  },
  ...devConfig,
  // More options: https://poi.js.org/#/options
});
