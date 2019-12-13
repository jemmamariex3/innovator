function buildConfig(env) {
    return require(`./configs/webpack.${env}.js`); 
}

module.exports = (env) => buildConfig(env === 'production' ? 'prod' : 'dev'); 