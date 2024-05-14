import { ReactElement, useState } from "react";
import LoginForm, { LoginReponseData } from "./LoginForm";
import NavBar from "./NavBar";
import NotificationManager, { NotificationData } from "./NotificationManager";
import AdminDashboard from "./AdminDashboard";

const App = () => {
	const addNotification = (notificationData: NotificationData) =>
		setNotificationQueue([...notificationQueue, notificationData]);

	const closeNotification = (index: number) =>
		setNotificationQueue(notificationQueue.filter((_, i) => i !== index));
	
	const completeLogin = (loginResponseData: LoginReponseData) => {

        setChildren([
            <AdminDashboard addNotification={addNotification} />
        ]);
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
