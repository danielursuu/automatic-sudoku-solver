import { Injectable, Logger } from "@nestjs/common";
import { Subject, Observable } from "rxjs";

import { RecognizerService } from "./recognizer.service";

@Injectable()
export class DataRecognizerService {

    private readonly logger = new Logger(DataRecognizerService.name, true);

    private queue: any[] = [];
    private ready = false;
    private output = new Subject<any>();

    constructor(
        private readonly recognizerService: RecognizerService
    ) { }

    public start() {
        this.recognizerService.startup();

        this.recognizerService.Response.subscribe((data) => {
            if (data.status === 'end') {
                this.recognizerService.endShell();
            }
            if (data.status === 'ready') {
                this.ready = true;
                this.process();
            } else {
                this.output.next(data);
                this.output = new Subject<any>();
            }
        });
    }

    public input(input) {
        this.queue.push(input);
        if (this.ready) {
            this.process();
        }
    }

    private process(): void {
        if (this.queue.length !== 0) {
            this.ready = false;
            this.recognizerService.process(this.queue.shift())
        }
    }

    public get Output(): Observable<any> {
        return this.output;
    }
}