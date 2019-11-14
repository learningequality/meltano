import React from 'react'
import moment from 'moment'

import { Timer } from '@/redash/app/components/Timer'

export default class ReactTest extends React.Component {
  render() {
    const time = moment().format()

    return (
      <div>
        <h1>Hello, World w/Angular + React in Vue</h1>

        <h2>React usage:</h2>
        <Timer from={time} />

        <h2>Angular usage:</h2>
        <rd-timer from={`"${time}"`} />
      </div>
    )
  }
}
