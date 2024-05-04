import { BACKEND_PATH } from './constants'
import "../css/Feature.css"


function Feature() {
    return (
        <div className="Feature-Container" >
            <a href={BACKEND_PATH + "movies"}>
                {BACKEND_PATH}movies

            </a>
        </div>
    );
}

export default Feature;