module.exports = {
  env: {
    browser: true,
    es6: true,
    node: true,
    mocha: true,
  },
  extends: [
    // add more generic rulesets here, such as:
    // 'eslint:recommended',
    'airbnb',
    'plugin:vue/recommended',
  ],
  rules: {
    // override/add rules settings here, such as:
    // 'vue/no-unused-vars': 'error'
    'no-plusplus': ['error', { allowForLoopAfterthoughts: true }],
  },
};
