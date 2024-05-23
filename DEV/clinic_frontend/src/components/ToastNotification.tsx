import Toast, { ToastProps } from "react-bootstrap/Toast";

interface ToastNotificationProps extends ToastProps {
    title: string;
    time?: string;
    message: string;
}

const ToastNotification = ({
    title,
    time = "",
    message,
    ...rest
}: ToastNotificationProps) => {
    return (
        <Toast {...rest}>
            <Toast.Header>
                <img
                    src="holder.js/20x20?text=%20"
                    className="rounded me-2"
                    alt=""
                />
                <strong className="me-auto">{title}</strong>
                <small>{time}</small>
            </Toast.Header>
            <Toast.Body>{message}</Toast.Body>
        </Toast>
    );
};

export default ToastNotification;
