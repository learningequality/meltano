import React from 'react'
import moment from 'moment'

import { Timer } from '@/redash/app/components/Timer'

export default class ReactTest extends React.Component {
  render() {
    const time = moment().format()

    return (
      <div>
        <h1>Hello, World w/Angular + React in Vue</h1>

        <hr />

        <h2>React usage:</h2>
        <Timer from={time} />

        <hr />

        <h2>Angular usage:</h2>
        <rd-timer from={`"${time}"`} />

        <hr />

        <h2>Angular+React Complex usage:</h2>
        <p>Stopping point = dual router crossroads. Options for next steps:</p>
        <div className="content">
          <ul>
            <li>Try having dual routers (Vue and now Angular). Scares me.</li>
            <li>
              Extracting Angular markup + corresponding controller subsets and
              converting to React (redash contribute back) or Vue
            </li>
          </ul>
        </div>
      </div>
    )
  }
}
