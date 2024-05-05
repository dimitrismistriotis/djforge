/* React template with variables from Allauth email_confirmation_message
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

interface DJForgeEmailConfirmationMessageProps {
    siteName?: string;
    activateURL?: string;
    displayYear?: string;
}

export const DJForgeEmailConfirmationMessage = ({
    siteName = "SITE_NAME_HERE",
    activateURL = "ACTIVATE_URL_HERE",
    displayYear = "YEAR_HERE",
}: DJForgeEmailConfirmationMessageProps) => {
    return (
        <Html>
            <Head />
            <Preview>Please Confirm your Email</Preview>

            <Body style={main}>
                <Container style={container}>
                    <Section style={logo}>
                        <Img width={114} src={`/static/logo_for_email.png`} />
                    </Section>
                    <Section style={sectionsBorders}>
                        <Row>
                            <Column style={sectionBorder} />
                            <Column style={sectionCenter} />
                            <Column style={sectionBorder} />
                        </Row>
                    </Section>
                    <Section style={content}>
                        <Text style={paragraph}>Hi from {siteName},</Text>
                        <Text style={paragraph}>
                            You are receiving this email because your email
                            address was given to register an account our
                            application.
                        </Text>
                        <Text style={paragraph}>
                            To confirm this is correct:
                        </Text>
                        <Text style={paragraph}>
                            <Tailwind>
                                <Text className="flex justify-center">
                                    <Link
                                        href={activateURL}
                                        className="bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-2 rounded-md"
                                    >
                                        Confirm Email
                                    </Link>
                                </Text>
                            </Tailwind>
                        </Text>
                        <Text style={paragraph}>
                            Alternatively copy and paste the follwing URL into
                            your browser:
                            <br />
                            {activateURL}
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

DJForgeEmailConfirmationMessage.PreviewProps = {
    siteName: "DJ Forge Site Name",
    activateURL: "{{ activate_url }}",
    displayYear: "202X",
} as DJForgeEmailConfirmationMessageProps;

export default DJForgeEmailConfirmationMessage;

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
