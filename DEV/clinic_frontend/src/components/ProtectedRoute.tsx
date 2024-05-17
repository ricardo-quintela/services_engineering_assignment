import { ReactElement } from "react";
import { Navigate } from "react-router-dom";
import { NotificationData } from "../interfaces/notification";

const ProtectedRoute = ({
    condition,
    redirectTo,
    addNotification,
    notificationData,
    children,
}: {
    condition: () => boolean;
    redirectTo: string;
    addNotification: (notificationData: NotificationData) => void;
    notificationData: NotificationData
    children: ReactElement;
}) => {
    if (!condition()) {
        addNotification(notificationData);
        return <Navigate to={redirectTo} replace />;
    }
    return children;
};

export default ProtectedRoute;
