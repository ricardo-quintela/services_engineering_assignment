import { useState } from "react";
import LoginForm from "./LoginForm";
import NavBar from "./NavBar";
import AdminDashboard from "./AdminDashboard";
import { NotificationData } from "../interfaces/notification";
import NotificationManager from "./NotificationManager";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import SchedullingForm from "./SchedullingForm";
import axios from "axios";

const App = () => {
    const addNotification = (notificationData: NotificationData) =>
        setNotificationQueue([...notificationQueue, notificationData]);

    const closeNotification = (index: number) =>
        setNotificationQueue(notificationQueue.filter((_, i) => i !== index));

    const [notificationQueue, setNotificationQueue] = useState(
        [] as NotificationData[]
    );

    return (
        <>
            {/* inner content of the page */}
            <BrowserRouter>
                {/* nav bar */}
                <NavBar />

                <section className="h-75">
					<Routes>
						<Route path="/" element={<h1>Página Inicial</h1>} />
						<Route path="/scheduling" element={<SchedullingForm />} />
						<Route
							path="/login"
							element={
								<LoginForm
									key={0}
									addNotification={addNotification}
								/>
							}
						/>
						<Route
							path="/admin"
							element={
								<AdminDashboard
									key={0}
									addNotification={addNotification}
								/>
							}
						/>
					</Routes>
				</section>

                {/* handle notifications */}
                <NotificationManager
                    notificationQueue={notificationQueue}
                    closeNotification={closeNotification}
                />
            </BrowserRouter>
        </>
    );
};

export default App;
