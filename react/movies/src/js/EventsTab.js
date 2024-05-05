import TabHeader from './TabHeader';
import "../css/Tabs.css"

function EventTab({ tab, setTab }) {
    const tabName = "Eventos"
    return (
        <div>
            {(tab == tabName || tab == "Escolhas") &&

                <TabHeader tabname={tabName} extraText={""} setTab={setTab} />
            }
            {
                tab == tabName &&
                <div className='TabBodyDiv'>

                    TODO Eventos
                    <button onClick={setTab.bind(this, "Escolhas")}>AAA</button>
                </div>
            }

        </div>
    )
}

export default EventTab