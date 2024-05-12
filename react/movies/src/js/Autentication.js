import { useState } from "react";
import { BACKEND_PATH,IMAGES_PATH } from './constants'
// import axios from "axios"
import "../css/Tabs.css"



function Autentication({ username, setUsername, isAutenticated, setIsAutenticated }) {
    const [password, setPassword] = useState('');
    const [msg, setMsg] = useState('');
    const [error, setError] = useState('');
    const [img,setImg] = useState('')

    const handleLogout = () => {
        setIsAutenticated(false)
        setMsg("")
    }

    const handleLogin = async (e) => {
        e.preventDefault();
        setMsg("Loading...")
        setError("")
        try {
            const response = await fetch(BACKEND_PATH + 'login/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ username, password }),
            });
            const data = await response.json();
            if (response.ok) {
                // Fez Login com sucesso
                // Guarda o token para invocações futuras durante a sessão
                localStorage.setItem('token', data.token);
                // Imprime msg de sucesso ou redireciona
                setImg(data.image)
                setMsg('Viva, fez login !');
                setIsAutenticated(true)
            } else {
                setMsg("")
                setError(data.error || 'Algo errado');
            }
        } catch (error) {
            console.error('Login falhou:', error);
            setError('Algo errado');
            setMsg("")
        }
    };

    if (isAutenticated) {
        return (
            <div className="auth" >
                <div>
                    <span style={{ fontWeight: "bold" }}>Username: </span>
                    {username}
                </div>
                <img alt="Not found" src={IMAGES_PATH+img}width={"10%"}/>
                <button onClick={handleLogout}>Logout</button>
            </div>
        )
    } else {
        return (
            <div className="auth">
                <h2>Login</h2>
                {error && <p>{error}</p>}
                {<p>{msg}</p>}
                <form onSubmit={handleLogin}>
                    <input
                        type="text"
                        placeholder="Username"
                        value={username}
                        onChange={(e) => setUsername(e.target.value)}
                    />
                    <input
                        type="password"
                        placeholder="Password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                    />
                    <button type="submit">Login</button>
                </form>
            </div>
        )
    }


}

export default Autentication;