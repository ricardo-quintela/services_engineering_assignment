import { useState } from "react";
import LoginForm from "./LoginForm";
import NavBar from "./NavBar";
import NotificationManager, { NotificationData } from "./NotificationManager";

const App = () => {
    const [notificationQueue, setNotificationQueue] = useState(
        [] as NotificationData[]
    );

    const addNotification = (notificationData: NotificationData) =>
        setNotificationQueue([...notificationQueue, notificationData]);

    const closeNotification = (index: number) => setNotificationQueue(notificationQueue.filter((_, i) => i !== index));

    return (
        <>
            <NavBar />
            <LoginForm addNotification={addNotification} />
            <NotificationManager notificationQueue={notificationQueue} closeNotification={closeNotification} />
        </>
    );
};

export default App;
