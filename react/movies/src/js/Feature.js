import { BACKEND_PATH } from './constants'
import "../css/Feature.css"


function Feature() {
    return (
        <div className="Feature-Container" >
            <a href={BACKEND_PATH.replace("/api","")}>
                Django app

            </a>
        </div>
    );
}

export default Feature;