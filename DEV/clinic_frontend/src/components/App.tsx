import { ReactElement, useState } from "react";
import LoginForm from "./LoginForm";
import NavBar from "./NavBar";
import AdminDashboard from "./AdminDashboard";
import { jwtDecode } from "jwt-decode";
import { useCookies } from "react-cookie";
import { NotificationData } from "../interfaces/notification";
import NotificationManager from "./NotificationManager";
import { JwtPayload } from "../interfaces/jwt";


const App = () => {
	const addNotification = (notificationData: NotificationData) =>
		setNotificationQueue([...notificationQueue, notificationData]);

	const closeNotification = (index: number) =>
		setNotificationQueue(notificationQueue.filter((_, i) => i !== index));

	const [cookies, setCookies] = useCookies(["jwt"]);
	
	const completeLogin = () => {

		const jwt_payload: JwtPayload = jwtDecode(cookies.jwt);
		console.table(jwt_payload);

		if (jwt_payload.role === "admin") {
			setChildren([
				<AdminDashboard key={0} addNotification={addNotification} />
			]);
		} else {
			setChildren([]);
		}

    };

	const [notificationQueue, setNotificationQueue] = useState([] as NotificationData[]
	);
	const [children, setChildren] = useState([
		<LoginForm
			key={0}
			addNotification={addNotification}
			completeLogin={completeLogin}
		/>
	] as ReactElement[]);

	

	return (
		<>
			<NavBar />

			{ children }

			<NotificationManager
				notificationQueue={notificationQueue}
				closeNotification={closeNotification}
			/>
		</>
	);
};

export default App;
