import fs from "fs";
import chalk from "chalk";
import TOML from "@iarna/toml";
import { version } from "../package.json";


const INFO = chalk.bold.hex('#000000').bgCyan(" INFO ");
const ERROR = chalk.bold.hex('#000000').bgRed(" ERROR ");


/**
 * 操作方式
 * 0: 仅更新小版本号（默认）
 * 1: 更新中版本号
 * 2: 更新大版本号
 */
const METHOD = parseInt(process.argv.slice(2)[0]) || 0;

/**
 * 根据指定的方法更新版本号
 * @param oldVersion - 旧版本号，格式为 "x.y.z"。
 * @returns 更新后的版本号。
 * @example 3.0.166-alpha -> 3.0.167-alpha
 */
const UpdateVersion = (oldVersion: string) => {
    const reg = /^(\d+)\.(\d+)\.(\d+)(-.*?)?$/;

    const match = oldVersion.match(reg) as RegExpMatchArray;

    const newVersion = match.slice(1, 4) as string[];
    const releaseType = match[4] || "";

    switch (METHOD) {
        case 0:
            newVersion[2] = (parseInt(newVersion[2]) + 1).toString();
            break;
        case 1:
            newVersion[1] = (parseInt(newVersion[1]) + 1).toString();
            newVersion[2] = "0";
            break;
        case 2:
            newVersion[0] = (parseInt(newVersion[0]) + 1).toString();
            newVersion[1] = "0";
            newVersion[2] = "0";
            break;
        default:
            break;
    }

    return [newVersion.join(".") + releaseType, newVersion.join(".")];
};

const [VERSION, PURE_VERSION] = UpdateVersion(version);


type TargetType = {
    /** 文件路径 */
    file: string,

    /** JSONPath */
    path: string,

    content: string,
}

const target: TargetType[] = [
    {
        file: "../package.json",
        path: "version",
        content: VERSION,
    },
    {
        file: "../BGsystem3-configure/package.json",
        path: "version",
        content: VERSION,
    },
    {
        file: "../BGsystem3-configure/src-tauri/tauri.conf.json",
        path: "package.version",
        content: PURE_VERSION,
    },
    {
        file: "../BGsystem3-configure/src-tauri/Cargo.toml",
        path: "package.version",
        content: PURE_VERSION,
    },
    {
        file: "../BGsystem3-timer/package.json",
        path: "version",
        content: VERSION,
    },
    {
        file: "../BGsystem3-timer/src-tauri/tauri.conf.json",
        path: "package.version",
        content: PURE_VERSION,
    },
    {
        file: "../BGsystem3-timer/src-tauri/Cargo.toml",
        path: "package.version",
        content: PURE_VERSION,
    },
    {
        file: "../BGsystem3-frontend/package.json",
        path: "version",
        content: VERSION,
    },
];


/**
 * 更新版本号
 * @param target 目标类型数组，包含文件和路径信息。
 */
const ChangeVersion = (target: TargetType[]) => {
    for (const { file, path, content } of target) {
        try {
            const data = fs.readFileSync(file, "utf-8");
            const fileType: "toml" | "json" = file.endsWith(".toml") ? "toml" : "json";

            const json = fileType == "json" ? JSON.parse(data) : TOML.parse(data);

            const paths = path.split(".");
            let obj = json;
            for (let i = 0; i < paths.length - 1; i++) {
                if (obj[paths[i]] === undefined) {
                    console.log(`文件 \`${chalk.underline(file)}\` 中不存在 JSON 对象 \`${chalk.underline(path)}\``);
                }
                obj = obj[paths[i]];
            }
            obj[paths[paths.length - 1]] = content;

            fs.writeFileSync(file,
                fileType === "json" ? JSON.stringify(json, null, 2) : TOML.stringify(json)
            );

            console.log(INFO, `文件 \`${chalk.underline(file)}\` 中 \`${chalk.underline(path)}\` 的版本号已更新为 \`${chalk.underline(VERSION)}\``);
        } catch (error) {
            console.log(ERROR, `${error}`);
        }
    };
};


if (require.main === module) {
    ChangeVersion(target);
}