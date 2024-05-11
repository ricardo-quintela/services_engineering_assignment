import axios from "axios";
import "bootstrap/dist/css/bootstrap.min.css";
import { FormEvent, useState } from "react";

axios.defaults.withCredentials = true;

function LoginForm() {

    const [message, setMessage] = useState("");

    const handleSubmit = (e: FormEvent) => {
        e.preventDefault();
        const payload = e.target as typeof e.target & {
            username: { value: string };
            password: { value: string };
        };


        axios.post(process.env.REACT_APP_API_URL + "login/", {
            username: payload.username.value,
            password: payload.password.value
        })
        .then(response => setMessage(
            response.data["message"] || response.data["error"]
        ));
    };

    return (
        <div className="d-flex justify-content-center align-items-center">
            <form onSubmit={handleSubmit}>
                <div className="mb-3">
                    <label htmlFor="username" className="form-label">
                        Username
                    </label>
                    <input type="text" className="form-control" id="username" />
                </div>
                <div className="mb-3">
                    <label htmlFor="password" className="form-label">
                        Password
                    </label>
                    <input
                        type="password"
                        className="form-control"
                        id="password"
                    />
                </div>

                <button type="submit" className="btn btn-primary">
                    Login
                </button>

                { message !== "" && <p>{ message }</p> }
            </form>
        </div>
    );
}

export default LoginForm;
