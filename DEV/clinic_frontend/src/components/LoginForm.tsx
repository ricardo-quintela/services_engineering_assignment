import axios from "axios";
import "bootstrap/dist/css/bootstrap.min.css";
import { FormEvent } from "react";
import { NotificationData } from "../interfaces/notification";

axios.defaults.withCredentials = true;

const LoginForm = ({
	addNotification,
	completeLogin,
}: {
	addNotification: (notificationData: NotificationData) => void;
	completeLogin: () => void;
}) => {
	const formInputs = {
		usernameInput: (
			<input type="text" className="form-control" id="username" />
		),
		passwordInput: (
			<input type="password" className="form-control" id="password" />
		),
	};

	const handleSubmit = (e: FormEvent) => {
		e.preventDefault();
		const payload = e.target as typeof e.target & {
			username: { value: string };
			password: { value: string };
		};

		axios
			.post(process.env.REACT_APP_API_URL + "login/", {
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

				if ("message" in response.data) completeLogin();
			})
			.catch(() =>
				addNotification({
					title: "Error",
					message: "An error has occured while attempting to login.",
				})
			);
	};

	return (
		<div className="d-flex flex-column gap-5 border p-5">
			<h1>Login</h1>
			<form
				className="d-flex flex-column justify-content-center align-items-center"
				onSubmit={handleSubmit}
			>
				<div className="mb-3">
					<label htmlFor="username" className="form-label">
						Username
					</label>
					{formInputs.usernameInput}
				</div>
				<div className="mb-3">
					<label htmlFor="password" className="form-label">
						Password
					</label>
					{formInputs.passwordInput}
				</div>

				<button type="submit" className="btn btn-primary">
					Login
				</button>
			</form>
		</div>
	);
};

export default LoginForm;
