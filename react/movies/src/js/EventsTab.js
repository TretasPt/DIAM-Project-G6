import TabHeader from './TabHeader';
import "../css/Tabs.css"
import { useEffect, useState } from 'react';
import axios from "axios"
import { BACKEND_PATH } from './constants'

function EventTab({ tab, setTab, group, setEvent, username }) {
    const tabName = "Eventos"


    const [eventList, setEventList] = useState([])


    function Event({ nome, pk }) {
        const onClick = () => {
            setTab("Escolhas");
            setEvent(pk)
        }
        return (
            <div className='TabElement'>
                <strong>Nome: </strong>{nome}
                <button onClick={onClick}>Selecionar</button>
            </div>
        )
    }

    useEffect(() => {
        if (group !== -1) {
            axios.post(BACKEND_PATH + "eventos/", { username: username, token: localStorage.getItem("token"), grupo: group })
                .then((r) => { setEventList(r.data) })
                .catch((e) => { console.log(e) })
        }
    },
        [group, tab, username])

    return (
        <div>
            {(tab === tabName || tab === "Escolhas") &&

                <TabHeader tabname={tabName} extraText={""} setTab={setTab} />
            }
            {
                tab === tabName &&
                <div className='TabBodyDiv'>
                    {eventList.length === 0 && <h4>Não existem eventos.</h4>}

                    {eventList.map((event) => (<Event nome={event.nome} pk={event.pk} key={event.pk} />))}

                </div>
            }

        </div>
    )
}

export default EventTab