import axios, { AxiosResponse } from "axios";
import {
    ChangeEvent,
    FormEvent,
    ReactElement,
    useState,
} from "react";
import { Container, Form } from "react-bootstrap";
import { NotificationData } from "../interfaces/notification";

const CameraFeed = ({
    addNotification,
    uploadTo,
    successHandler,
    aditionalFormInputs = [],
}: {
    addNotification: (notificationData: NotificationData) => void;
    uploadTo: string;
    successHandler: (response: AxiosResponse) => void;
    aditionalFormInputs?: {
        inputLabel: string;
        inputField: ReactElement;
    }[];
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

        Array.from(e.currentTarget.children[0].children)
            .filter((_, index) => index % 2 === 1)
            .map((element) => element as HTMLInputElement)
            .forEach((element) => formData.append(element.id, element.value));

        axios
            .post(process.env.REACT_APP_API_URL + uploadTo, formData)
            .then((response) => successHandler(response))
            .catch((response) => {
                addNotification({
                    title: "Error",
                    message:
                        "error" in response.data
                            ? response.data["error"]
                            : "An error has occurred.",
                });
            });
    };

    return (
        <Container className="border p-3">
            <h2>Carregar Imagem</h2>

            <Form
                onSubmit={handleSubmit}
                className="d-flex flex-column align-items-center gap-3"
                id="ikd-man"
            >
                {aditionalFormInputs.length > 0 && (
                    <Container className="d-flex flex-column">
                        {aditionalFormInputs.map((input) => (
                            <>
                                <Form.Label
                                    htmlFor={input.inputField.props["id"]}
                                >
                                    {input.inputLabel}
                                </Form.Label>
                                {input.inputField}
                            </>
                        ))}
                    </Container>
                )}

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
