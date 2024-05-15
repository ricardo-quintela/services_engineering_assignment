import "bootstrap/dist/css/bootstrap.min.css";
import ToastNotification from "./ToastNotification";
import { NotificationData } from "../interfaces/notification";

const NotificationManager = ({
    notificationQueue,
    closeNotification,
}: {
    notificationQueue: NotificationData[];
    closeNotification: (index: number) => void;
}) => {
    return (
        <div className="position-absolute end-0 me-5 bottom-0 mb-5">
            {notificationQueue.map((notificationData, index) => (
                <ToastNotification
                    key={index}
                    title={notificationData.title}
                    time={notificationData.time}
                    message={notificationData.message}
                    onClose={() => closeNotification(index)}
                />
            ))}
        </div>
    );
};

export default NotificationManager;
