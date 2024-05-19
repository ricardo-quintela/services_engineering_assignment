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
    uploadTo
}: {
    addNotification: (notificationData: NotificationData) => void;
    uploadTo: string;
}) => {
    const [files, setFiles] = useState<FileList | null>(null);

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
            .post(process.env.REACT_APP_API_URL + uploadTo, formData)
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
