import TabHeader from './TabHeader';
import "../css/Tabs.css"

function GroupTab({ tab, setTab }) {
    const tabName = "Grupos";
    return (
        <div>
            <TabHeader tabname={tabName} extraText={""} setTab={setTab} />
            {
                tab == tabName &&
                <div className='TabBodyDiv'>

                    TODO Grupos
                    <button onClick={setTab.bind(this,"Eventos")}>AAA</button>
                </div>
            }

        </div>
    )
}

export default GroupTab