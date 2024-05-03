/* React template with variables from Allauth PasswordResetKeyMessage
 */
import {
    Body,
    Container,
    Column,
    Head,
    Html,
    Img,
    Link,
    Preview,
    Row,
    Section,
    Text,
    Tailwind,
} from "@react-email/components";
import * as React from "react";

interface DJForgePasswordResetKeyMessageProps {
    username?: string;
    updatedDate?: Date;
    currentYear?: number;
    baseUrl?: string;
}

export const DJForgePasswordResetKeyMessage = ({
    username,
    updatedDate,
    currentYear,
    baseUrl,
}: DJForgePasswordResetKeyMessageProps) => {
    if (!baseUrl) {
        baseUrl = process.env.VERCEL_URL
            ? `https://${process.env.VERCEL_URL}`
            : "";
    }

    const formattedDate = new Intl.DateTimeFormat("en", {
        dateStyle: "medium",
        timeStyle: "medium",
    }).format(updatedDate);

    const displayYear = currentYear || new Date().getFullYear();

    return (
        <Html>
            <Head />
            <Preview>You updated the password for your Twitch account</Preview>
            <Body style={main}>
                <Container style={container}>
                    <Section style={logo}>
                        <Img
                            width={114}
                            src={`${baseUrl}/static/dj-logo_for_email.png`}
                        />
                    </Section>
                    <Section style={sectionsBorders}>
                        <Row>
                            <Column style={sectionBorder} />
                            <Column style={sectionCenter} />
                            <Column style={sectionBorder} />
                        </Row>
                    </Section>
                    <Section style={content}>
                        <Text style={paragraph}>Hi {username},</Text>
                        <Text style={paragraph}>
                            Asked to update your password on {formattedDate}. If
                            this was you, then no further action is required.
                        </Text>
                        <Text style={paragraph}>
                            However if you did NOT perform this password change,
                            please{" "}
                            <Link href="#" style={link}>
                                reset your account password
                            </Link>{" "}
                            immediately.
                        </Text>
                        <Text style={paragraph}>
                            Remember to use a password that is both strong and
                            unique to your account. To learn more about how to
                            create a strong and unique password,{" "}
                            <Link href="#" style={link}>
                                click here.
                            </Link>
                        </Text>
                        <Text style={paragraph}>
                            Still have questions? Please contact{" "}
                            <Link href="#" style={link}>
                                Support
                            </Link>
                        </Text>
                        <Text style={paragraph}>
                            Thanks,
                            <br />
                            The DJ Forge Team
                        </Text>
                    </Section>
                </Container>

                <Container style={container}>
                    <Section style={content}>
                        <Tailwind>
                            <Text className="flex justify-center">
                                <Link
                                    href="#"
                                    className="bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-2 rounded-md"
                                >
                                    Click this button for something to happen.
                                </Link>
                            </Text>
                        </Tailwind>
                    </Section>
                </Container>

                <Section style={footer}>
                    <Row>
                        <Text style={{ textAlign: "center", color: "#706a7b" }}>
                            © {displayYear} DJ Forge
                        </Text>
                    </Row>
                </Section>
            </Body>
        </Html>
    );
};

//
// Properties as Django template variables
//
DJForgePasswordResetKeyMessage.PreviewProps = {
    username: "{{ username }}",
    reset_url: "{{ password_reset_url }}",
} as DJForgePasswordResetKeyMessageProps;

export default DJForgePasswordResetKeyMessage;

const fontFamily = "HelveticaNeue,Helvetica,Arial,sans-serif";

const main = {
    backgroundColor: "#efeef1",
    fontFamily,
};

const paragraph = {
    lineHeight: 1.5,
    fontSize: 14,
};

const container = {
    maxWidth: "580px",
    margin: "30px auto",
    backgroundColor: "#ffffff",
};

const footer = {
    maxWidth: "580px",
    margin: "0 auto",
};

const content = {
    padding: "5px 20px 10px 20px",
};

const logo = {
    display: "flex",
    justifyContent: "center",
    alingItems: "center",
    padding: 30,
};

const sectionsBorders = {
    width: "100%",
    display: "flex",
};

const sectionBorder = {
    borderBottom: "1px solid rgb(238,238,238)",
    width: "249px",
};

const sectionCenter = {
    borderBottom: "1px solid rgb(145,71,255)",
    width: "102px",
};

const link = {
    textDecoration: "underline",
};
