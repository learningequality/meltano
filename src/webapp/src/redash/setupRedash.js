import angular from 'angular'

export default function setup() {
  const ngModule = angular.module('app', [])

  // Smallest subset of redash/client/app/config/index.js to boot Redash Angular
  console.log('TODO register timer component properly')

  ngModule.run(() => {})
}
