import React from 'react'
import moment from 'moment'

import { Timer } from '@/redash/Timer'

export default class ReactTest extends React.Component {
  render() {
    return (
      <div>
        <h1>Hello, World w/ReactTest</h1>
        <h2>React usage:</h2>
        <Timer from={moment().format()} />
        <h2>Angular usage:</h2>
        {/* <rd-timer from="queryResult.getUpdatedAt()"></rd-timer> */}
      </div>
    )
  }
}
