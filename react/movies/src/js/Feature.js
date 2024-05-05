import { BACKEND_PATH } from './constants'
import "../css/Feature.css"
import { useState } from 'react';
import GroupTab from './GroupsTab';
import EventsTab from './EventsTab';
import ChoicesTab from './ChoicesTab';


function Feature({ username }) {

    const [tab, setTab] = useState("Grupos")//Values will be "Grupos","Eventos" or "Escolhas"

    return (
        <div className="Feature-Container" >
            <a href={BACKEND_PATH.replace("/api", "")}>
                Django app
            </a>
            {tab}
            {username}
            <GroupTab setTab={setTab} tab={tab}/>
            <EventsTab setTab={setTab} tab={tab}/>
            <ChoicesTab setTab={setTab} tab={tab}/>
        </div>
    );
}

export default Feature;