import { jwtDecode } from "jwt-decode";
import { NotificationData } from "../interfaces/notification";
import CameraFeed from "./CameraFeed";
import { JwtPayload } from "../interfaces/jwt";
import { Container } from "react-bootstrap";

const Profile = ({
    addNotification,
}: {
    addNotification: (notificationData: NotificationData) => void;
}) => {
    return (
        <Container className="d-flex flex-column gap-3">
            <h1>
                Perfil de{" "}
                {
                    (jwtDecode(localStorage.getItem("jwt") || "") as JwtPayload)
                        .username
                }
            </h1>
            <CameraFeed addNotification={addNotification} />
        </Container>
    );
};

export default Profile;
