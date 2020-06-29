import { Injectable, Logger } from "@nestjs/common";
import { Subject, Observable } from "rxjs";
import { SolverService } from "./solver.service";

@Injectable()
export class DataSolverService {

    private readonly logger = new Logger(DataSolverService.name, true);

    private queue: any[] = [];
    private ready = false;
    private output = new Subject<any>();

    constructor(
        private readonly solverService: SolverService
    ) { }

    public start() {
        this.solverService.startup();
        this.solverService.Response.subscribe((data) => {
            if (data.status === 'end') {
                this.solverService.endShell();
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
            this.solverService.process(this.queue.shift())
        }
    }

    public get Output(): Observable<any> {
        return this.output;
    }
}