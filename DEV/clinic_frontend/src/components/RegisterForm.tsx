import axios from "axios";
import "bootstrap/dist/css/bootstrap.min.css";
import { FormEvent } from "react";
import { NotificationData } from "../interfaces/notification";
import { useNavigate } from "react-router-dom";

const RegisterForm = ({
    addNotification,
}: {
    addNotification: (notificationData: NotificationData) => void;
}) => {
    const formInputs = {
        usernameInput: (
            <input type="text" className="form-control" id="username" />
        ),
        passwordInput: (
            <input type="password" className="form-control" id="password" />
        ),
    };

    const navigate = useNavigate();

    const handleSubmit = (e: FormEvent) => {
        e.preventDefault();
        const payload = e.target as typeof e.target & {
            username: { value: string };
            password: { value: string };
        };

        axios
            .post(process.env.REACT_APP_API_URL + "register/", {
                username: payload.username.value,
                password: payload.password.value,
            })
            .then((response) => {
                addNotification({
                    title: "message" in response.data ? "Success" : "Error",
                    message:
                        "message" in response.data
                            ? response.data["message"]
                            : response.data["error"],
                });
                if ("message" in response.data) {
                    navigate("/");
                }
            })
            .catch(() => {
                addNotification({
                    title: "Error",
                    message: "An error has occured while attempting to login.",
                });
            });
    };

    return (
        <div className="d-flex flex-column gap-5 border p-5">
            <h1>Registar</h1>
            <form
                className="d-flex flex-column justify-content-center align-items-center"
                onSubmit={handleSubmit}
            >
                <div className="mb-3">
                    <label htmlFor="username" className="form-label">
                        Nome de Utilizador
                    </label>
                    {formInputs.usernameInput}
                </div>
                <div className="mb-3">
                    <label htmlFor="password" className="form-label">
                        Palavra-passe
                    </label>
                    {formInputs.passwordInput}
                </div>

                <button type="submit" className="btn btn-primary">
                    Entrar
                </button>
            </form>
        </div>
    );
};

export default RegisterForm;
