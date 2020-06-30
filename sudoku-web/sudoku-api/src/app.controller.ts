import { Controller, Get, Post, UseInterceptors, UploadedFile, Param, Res, Logger, Body } from '@nestjs/common';
import { FileInterceptor } from '@nestjs/platform-express';
import { diskStorage } from 'multer';

import { AppService } from './app.service';
import { imageFileFilter, editFileName } from './utils/image-uploading.utils';
import { DataSolverService } from './shared/data-solver.service';
import { DataRecognizerService } from './shared/data-recognizer.service';

@Controller()
export class AppController {

  private readonly logger = new Logger(AppController.name, true);

  constructor(
    private readonly appService: AppService,
    private readonly dataSolverService: DataSolverService,
    private readonly dataRecognizerService: DataRecognizerService
  ) { }

  @Get()
  getHello(): string {
    return this.appService.getHello();
  }

  @Post('upload')
  @UseInterceptors(FileInterceptor('file', {
    storage: diskStorage({
      destination: '../sudoku-ui/src/assets/',
      filename: editFileName
    }),
    fileFilter: imageFileFilter,
  })
  )
  async uploadImage(@UploadedFile() file, @Res() res) {
    this.logger.log("Image Uploaded!");

    this.dataRecognizerService.start();
    this.dataRecognizerService.input(file.filename);
    this.dataRecognizerService.Output.subscribe((output => {
      this.logger.log(output);
      res.send({ board: output, fileName: file.filename });
    }))
  }

  @Post('validate')
  validateSudokuSolver(@Body() board: number[][], @Res() res) {
    this.logger.log("Board validated!");

    this.dataSolverService.start();
    this.dataSolverService.input(board);
    this.dataSolverService.Output.subscribe((output) => {
      this.logger.log(output);
      res.send({ board: output });
    })
  }

  @Get(':path')
  getUploadedImage(@Param('path') path, @Res() res) {
    return res.sendFile(path, { root: './images' });
  }
}
