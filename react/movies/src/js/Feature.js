// import { BACKEND_PATH } from './constants'
import "../css/Feature.css"
import { useState } from 'react';
import GroupTab from './GroupsTab';
import EventsTab from './EventsTab';
import ChoicesTab from './ChoicesTab';


function Feature({ username }) {

    const [tab, setTab] = useState("Grupos")//Values will be "Grupos","Eventos" or "Escolhas"

    const [group, setGroup] = useState(-1)
    const [event, setEvent] = useState(-1)

    return (
        <div className="Feature-Container" >
            <GroupTab setTab={setTab} tab={tab} username={username} setGroup={setGroup} />
            <EventsTab setTab={setTab} tab={tab} group={group} setEvent={setEvent} username={username} />
            <ChoicesTab setTab={setTab} tab={tab} event={event} username={username} />
        </div>
    );
}

export default Feature;