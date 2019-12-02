/*
   This module handles the Flask context,
   either set by the Meltano API in production
   or from webpack in development.
*/

module.exports = function() {
  return (
    window.FLASK || {
      airflowUrl: process.env.AIRFLOW_URL,
      appUrl: process.env.MELTANO_WEBAPP_URL,
      dbtDocsUrl: process.env.DBT_DOCS_URL,
      isSendAnonymousUsageStats: false,
      projectId: 'none',
      // Update if we make a TOS update and require another acknowledgement for each UI user
      termsOfServiceVersion: 1.0,
      version: 'source'
    }
  )
}
