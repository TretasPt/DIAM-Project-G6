import TabHeader from './TabHeader';
import "../css/Tabs.css"

function ChoicesTab({ tab, setTab }) {
    const tabName = "Escolhas";
    return (
        <div>
            {tab == tabName &&

                <TabHeader tabname={tabName} extraText={""} setTab={setTab} />
            }            {
                tab == tabName &&
                <div className='TabBodyDiv TabLast'>
                    TODO Escolhas
                </div>
            }
        </div>
    )
}

export default ChoicesTab