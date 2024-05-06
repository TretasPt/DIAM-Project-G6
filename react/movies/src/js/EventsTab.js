import TabHeader from './TabHeader';
import "../css/Tabs.css"
import { useEffect, useState } from 'react';
import axios from "axios"
import { BACKEND_PATH } from './constants'

function EventTab({ tab, setTab, group, setEvent, username }) {
    const tabName = "Eventos"


    const [eventList, setEventList] = useState([])

    const getEventList = () => {
        axios.post(BACKEND_PATH + "eventos/", { username: username, token: localStorage.getItem("token"), grupo: group })
            .then((r) => {setEventList(r.data) })
            .catch((e) => { console.log(e) })
    }

    function Event({ nome, pk }) {
        const onClick = () => {
            setTab("Escolhas");
            setEvent(pk)
        }
        return (
            <div>
                <h5>Nome: {nome}</h5>
                <button onClick={onClick}>Selecionar</button>
            </div>
        )
    }

    useEffect(() => {
        if (group != -1) {
            getEventList()
        }
    },
        [group, tab])

    return (
        <div className='TabElement'>
            {(tab == tabName || tab == "Escolhas") &&

                <TabHeader tabname={tabName} extraText={""} setTab={setTab} />
            }
            {
                tab == tabName &&
                <div className='TabBodyDiv'>

                    {/* TODO Eventos
                    <button onClick={setTab.bind(this, "Escolhas")}>AAA</button> */}
                    {eventList.map((event) => (<Event nome={event.nome} pk={event.pk} key={event.pk} />))}

                </div>
            }

        </div>
    )
}

export default EventTab