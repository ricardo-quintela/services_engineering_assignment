import { jwtDecode } from "jwt-decode";
import { NotificationData } from "../interfaces/notification";
import CameraFeed from "./CameraFeed";
import { JwtPayload } from "../interfaces/jwt";
import { Container } from "react-bootstrap";
import { AxiosResponse } from "axios";

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
            <CameraFeed
                addNotification={addNotification}
                uploadTo="image/"
                successHandler={(response: AxiosResponse) =>
                    addNotification({
                        title: "message" in response.data ? "Success" : "Error",
                        message:
                            "message" in response.data
                                ? response.data["message"]
                                : response.data["error"],
                    })
                }
            />
        </Container>
    );
};

export default Profile;
