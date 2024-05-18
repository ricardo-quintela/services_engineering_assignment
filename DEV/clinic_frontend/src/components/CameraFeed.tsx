import axios from "axios";
import {
    ChangeEvent,
    FormEvent,
    createRef,
    useEffect,
    useRef,
    useState,
} from "react";
import { Button, Container, Form } from "react-bootstrap";
import { NotificationData } from "../interfaces/notification";

const CameraFeed = ({
    addNotification,
}: {
    addNotification: (notificationData: NotificationData) => void;
}) => {
    const videoRef = useRef<any>(null);
    const photoRef = useRef<any>(null);

    const [deviceFound, setDeviceFound] = useState(true);
    const [hasPhoto, setHasPhoto] = useState(false);
    const [files, setFiles] = useState<FileList | null>(null);

    const getVideo = () => {
        navigator.mediaDevices
            .getUserMedia({ video: { width: 1920, height: 1080 } })
            .then((stream) => {
                if (videoRef.current === null) return;

                let video = videoRef.current;
                video.srcObject = stream;
                video.play();
            })
            .catch(() => setDeviceFound(false));
    };

    useEffect(() => {
        getVideo();
    }, [videoRef]);

    const fileSelectedHandler = (event: ChangeEvent<HTMLInputElement>) => {
        setFiles(event.target.files);
    };

    const handleSubmit = (e: FormEvent) => {
        e.preventDefault();

        if (files === null) {
            addNotification({
                title: "Carregar imagem",
                message: "Não foram carregados arquivos",
            });
            return;
        }

        const formData = new FormData();
        formData.append("file", files[0], files[0].name);

        axios
            .post(process.env.REACT_APP_API_URL + "image/", formData)
            .then((response) => {
                addNotification({
                    title: "message" in response.data ? "Success" : "Error",
                    message:
                        "message" in response.data
                            ? response.data["message"]
                            : response.data["error"],
                });

            })
            .catch(() => {
                addNotification({
                    title: "Error",
                    message: "An error has occured while attempting to login.",
                });
            });
    };

    return (
        <Container className="border p-3">
            <h2>Carregar Imagem</h2>
            {deviceFound && (
                <>
                    <Container>
                        <video ref={videoRef} />
                        <Button>SNAP</Button>
                    </Container>
                    <Container
                        className={"result" + (hasPhoto ? "-photo" : "")}
                    >
                        <canvas ref={photoRef} />
                        <Button>Close</Button>
                    </Container>
                    <p>OU</p>
                </>
            )}

            <Form
                onSubmit={handleSubmit}
                className="d-flex flex-column align-items-center gap-3"
            >
                <Container>
                    <Form.Label htmlFor="selectImage">Imagem</Form.Label>
                    <Form.Control
                        type="file"
                        id="selectImage"
                        accept="image/jpeg"
                        onChange={fileSelectedHandler}
                    ></Form.Control>
                    <Form.Text>
                        A imagem deve ser no formato JPEG (.jpg ou .jpeg) e não
                        deve ultrapassar os 25Kb
                    </Form.Text>
                </Container>
                <button type="submit" className="btn btn-primary">
                    Enviar
                </button>
            </Form>
        </Container>
    );
};

export default CameraFeed;
