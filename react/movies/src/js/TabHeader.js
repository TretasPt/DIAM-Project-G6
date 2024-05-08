import "../css/Tabs.css"

function TabHeader({tabname,extraText,setTab}){
    return (
        <div className="TabHeaderDiv" onClick={()=>setTab(tabname)}>
            <h3>{tabname}</h3>
            <h5>{extraText}</h5>
        </div>
    )
}

export default TabHeader;