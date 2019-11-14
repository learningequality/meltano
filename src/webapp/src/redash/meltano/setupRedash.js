import angular from 'angular'

import { isFunction } from 'lodash'

export default function setup() {
  const ngModule = angular.module('app-design', [])

  function registerAll(context) {
    const modules = context
      .keys()
      .map(context)
      .map(module => module.default)

    return modules
      .filter(isFunction)
      .filter(f => f.init)
      .map(f => f(ngModule))
  }

  function registerComponents() {
    // We repeat this code in other register functions, because if we don't use a literal for the path
    // Webpack won't be able to statcily analyze our imports.
    const context = require.context(
      '@/redash/app/components',
      true,
      /^((?![\\/.]test[\\./]).)*\.jsx?$/
    )
    registerAll(context)
  }

  registerComponents()

  ngModule.run(() => {
    console.log('init angular app')
  })
}
