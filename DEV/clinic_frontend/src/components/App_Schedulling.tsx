// Navbar
// Formulário
// Notification

import { useState } from "react";
import NavBar from "./NavBar";
import NotificationManager from "./NotificationManager";
import SchedullingForm from "./SchedullingForm";
import { NotificationData } from "../interfaces/notification";

const App_Schedulling = () => {
    const [notificationQueue, setNotificationQueue] = useState(
        [] as NotificationData[]
    );

    const addNotification = (notificationData: NotificationData) =>
        setNotificationQueue([...notificationQueue, notificationData]);

    const closeNotification = (index: number) => setNotificationQueue(notificationQueue.filter((_, i) => i !== index));

    return (
        <>
            <NavBar />
            <h1 className="p-4"> Marcação de Consulta </h1>
            <SchedullingForm />
            <NotificationManager notificationQueue={notificationQueue} closeNotification={closeNotification} />
        </>
    );
};

export default App_Schedulling;