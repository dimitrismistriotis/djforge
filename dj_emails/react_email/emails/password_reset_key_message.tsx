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
    baseUrl?: string;
    username?: string;
    resetUrl?: string;
    displayYear?: string;
}

export const DJForgePasswordResetKeyMessage = ({
    baseUrl = "BASE_URL_HERE",
    username = "USERNAME_HERE",
    resetUrl = "RESET_URL_HERE",
    displayYear = "YEAR_HERE",
}: DJForgePasswordResetKeyMessageProps) => {
    return (
        <Html>
            <Head />
            <Preview>Password Reset Request</Preview>
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
                            You're receiving this email because you or someone
                            else has requested a password reset for your user
                            account. It can be safely ignored if you did not
                            request a password reset. Click the link below to
                            reset your password.
                        </Text>
                        <Text style={paragraph}>
                            <Tailwind>
                                <Text className="flex justify-center">
                                    <Link
                                        href={resetUrl}
                                        className="bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-2 rounded-md"
                                    >
                                        Reset Your Password
                                    </Link>
                                </Text>
                            </Tailwind>
                        </Text>
                        <Text style={paragraph}>
                            Alternatively copy and paste the follwing URL into
                            your browser:
                            <br />
                            {resetUrl}
                        </Text>
                        <Text style={paragraph}>
                            Thanks,
                            <br />
                            The DJ Forge Team
                        </Text>
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
    baseUrl: "{{SITE_URL}}",
    username: "{{ username }}",
    resetUrl: "{{ password_resetUrl }}",
    displayYear: '{% now "Y" %}',
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
