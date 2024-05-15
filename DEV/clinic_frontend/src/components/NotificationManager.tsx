import "bootstrap/dist/css/bootstrap.min.css";
import ToastNotification from "./ToastNotification";
import { NotificationData } from "../interfaces/notification";
import { ToastContainer } from "react-bootstrap";

const NotificationManager = ({
    notificationQueue,
    closeNotification,
}: {
    notificationQueue: NotificationData[];
    closeNotification: (index: number) => void;
}) => {
    return (
        <ToastContainer className="me-2 mb-2" position="bottom-end">
            {notificationQueue.map((notificationData, index) => (
                <ToastNotification
                    key={index}
                    title={notificationData.title}
                    time={notificationData.time}
                    message={notificationData.message}
                    onClose={() => closeNotification(index)}
                />
            ))}
        </ToastContainer>
    );
};

export default NotificationManager;
