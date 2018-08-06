const HtmlWebpackIncludeAssetsPlugin = require('html-webpack-include-assets-plugin');
const HtmlWebpackInlineSourcePlugin = require('html-webpack-inline-source-plugin');
module.exports = {
    chainWebpack: config => {
        if (process.env.NODE_ENV === 'production') {
            config.plugin('html-assets').use(HtmlWebpackIncludeAssetsPlugin)
            config.plugin('html-assets').tap(args => {
                args[0].assets = ['css/bootstrap.min.css', 'css/bootstrap.min.css.map', 'js/jquery-3.3.1.slim.min.js', 'js/popper.min.js', 'bootstrap.min.js']
                args[0].append = false
                return args
            })
            config.plugin('html-inline').use(HtmlWebpackInlineSourcePlugin)
            config.plugin('html').tap(args => {
                args[0].inlineSource = '.(js|css)$'
                return args
            })
        }
    }
}
