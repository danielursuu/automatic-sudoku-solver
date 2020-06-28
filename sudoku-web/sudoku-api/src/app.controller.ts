import { Controller, Get, Post, UseInterceptors, UploadedFile, Param, Res, Logger } from '@nestjs/common';
import { FileInterceptor } from '@nestjs/platform-express';
import { diskStorage } from 'multer';

import { AppService } from './app.service';
import { imageFileFilter, editFileName } from './utils/image-uploading.utils';
import { PythonService } from './shared/python.service';
import { DataService } from './shared/data.service';

@Controller()
export class AppController {

  private readonly logger = new Logger(AppController.name, true);

  constructor(
    private readonly appService: AppService,
    private readonly dataService: DataService
  ) {
    this.dataService.Output.subscribe((output => {
      this.logger.log(output);
    }))
  }

  @Get()
  getHello(): string {
    return this.appService.getHello();
  }

  @Post('upload')
  @UseInterceptors(
    FileInterceptor('image', {
      storage: diskStorage({
        destination: './images',
        filename: editFileName
      }),
      fileFilter: imageFileFilter,
    })
  )
  async uploadImage(@UploadedFile() file) {
    console.log("Uploaded!");

    const response = {
      originalName: file.originalname,
      fileName: file.filename
    };
    return response;
  }

  @Get(':path')
  getUploadedImage(@Param('path') path, @Res() res) {
    return res.sendFile(path, { root: './images' });
  }
}
